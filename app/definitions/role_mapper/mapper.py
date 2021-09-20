import os
import yaml
import pathlib
import click
import itertools as it
from flask import Flask
from config import Config

from app.definitions.exceptions import AppException
from app.services.keycloak_service import AuthService

auth_service = AuthService()
service_name = Config.SERVICE_NAME


def init_app(app: Flask):
    @app.cli.command("map_roles")
    @click.option("--blueprint", "-b", "blueprint")
    def map_roles(blueprint):
        with app.test_request_context():
            path = app.instance_path
            file = os.path.join(path, "roles.yml")
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
            previous_roles = get_yaml_data(file)
            previous_role_set = set()

            if blueprint is None:
                view_dict = no_blueprint_map(app)
                if previous_roles:
                    previous_role_set = set(it.chain(*previous_roles.values()))
                current_role_set = set(it.chain(*view_dict.values()))
                deleted_roles = previous_role_set.difference(current_role_set)
                added_roles = current_role_set.difference(previous_role_set)
                remove_roles_from_keycloak(deleted_roles)
                add_roles_to_keycloak(added_roles)
            else:
                view_dict = with_blueprint_map(app, blueprint)
                if previous_roles:
                    previous_role_set = set(previous_roles.get(blueprint))
                current_role_set = set(view_dict.get(blueprint))
                deleted_roles = previous_role_set.difference(current_role_set)
                added_roles = current_role_set.difference(previous_role_set)
                remove_roles_from_keycloak(deleted_roles)
                add_roles_to_keycloak(added_roles)
                previous_roles[blueprint] = list(current_role_set)
            export_to_yml(file, view_dict)


def with_blueprint_map(app, blueprint):
    view_dict = {}
    for fn_name in app.view_functions:
        name = fn_name.split(".")
        blueprint_name = name[0]
        if blueprint_name == blueprint:
            func_name = name[1]
            if blueprint_name in view_dict:
                view_dict[blueprint_name].append(func_name)
            else:
                view_dict[blueprint_name] = [func_name]
    return view_dict


def no_blueprint_map(app):
    view_dict = {}
    for fn_name in app.view_functions:
        if fn_name == "static" or fn_name == "create_swagger_spec":
            continue
        name = fn_name.split(".")

        blueprint_name = name[0]
        func_name = name[1]

        if blueprint_name == "swagger_ui":
            continue

        if blueprint_name in view_dict:
            view_dict[blueprint_name].append(func_name)
        else:
            view_dict[blueprint_name] = [func_name]

    return view_dict


def export_to_yml(file_name, value):
    with open(file_name, "w") as out:
        yaml.dump(value, out)


def get_yaml_data(file_name):
    with open(file_name, "r") as out:
        python_object = yaml.load(out, Loader=yaml.SafeLoader)
        return python_object


def get_filtered_data(file_name, key):
    data = get_yaml_data(file_name)
    return data.get(key)


def add_roles_to_keycloak(roles):
    for role in roles:
        try:
            auth_service.create_role(service_name + "_" + role)
            print(f"{role} created successfully")

        except AppException.KeyCloakAdminException as e:
            print(e.context)


def remove_roles_from_keycloak(roles):
    for role in roles:
        try:
            auth_service.delete_role(service_name + "_" + role)
            print(f"{role} deleted successfully")

        except AppException.KeyCloakAdminException as e:
            print(e.context)
