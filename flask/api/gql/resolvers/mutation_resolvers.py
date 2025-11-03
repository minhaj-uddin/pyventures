from ariadne import MutationType
from graphql import GraphQLError

from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    get_jwt_identity, get_jwt, jwt_required,
    verify_jwt_in_request
)

from gql.db import db
from gql.models import StoreModel, ItemModel, TagModel, UserModel
from gql.models.user import UserRole
from gql.blocklist import BLOCKLIST

mutation = MutationType()


# ---------------- Store ----------------
@mutation.field("createStore")
def resolve_create_store(_, info, name):
    verify_jwt_in_request()
    user_claims = get_jwt()
    if user_claims.get("role") != "admin":
        raise GraphQLError("Admin privilege required.")
    store = StoreModel(name=name)
    db.session.add(store)
    db.session.commit()
    return store


@mutation.field("deleteStore")
def resolve_delete_store(_, info, id):
    verify_jwt_in_request()
    user_claims = get_jwt()
    if user_claims.get("role") != "admin":
        raise GraphQLError("Admin privilege required.")
    store = StoreModel.query.get(id)
    if not store:
        raise GraphQLError("Store not found.")
    db.session.delete(store)
    db.session.commit()
    return {"message": "Store deleted."}


# ---------------- Item ----------------
@mutation.field("createItem")
def resolve_create_item(_, info, name, description, price, storeId):
    item = ItemModel(name=name, description=description,
                     price=price, store_id=storeId)
    db.session.add(item)
    db.session.commit()
    return item


@mutation.field("updateItem")
def resolve_update_item(_, info, id, name=None, price=None):
    item = ItemModel.query.get(id)
    if not item:
        raise GraphQLError("Item not found.")
    if name:
        item.name = name
    if price:
        item.price = price
    db.session.commit()
    return item


@mutation.field("deleteItem")
def resolve_delete_item(_, info, id):
    verify_jwt_in_request()
    user_claims = get_jwt()
    if user_claims.get("role") != "admin":
        raise GraphQLError("Admin privilege required.")
    item = ItemModel.query.get(id)
    if not item:
        raise GraphQLError("Item not found.")
    db.session.delete(item)
    db.session.commit()
    return {"message": "Item deleted."}


# ---------------- Tag ----------------
@mutation.field("createTag")
def resolve_create_tag(_, info, storeId, name):
    tag = TagModel(name=name, store_id=storeId)
    db.session.add(tag)
    db.session.commit()
    return tag


@mutation.field("deleteTag")
def resolve_delete_tag(_, info, id):
    tag = TagModel.query.get(id)
    if not tag:
        raise GraphQLError("Tag not found.")
    if tag.items:
        raise GraphQLError("Cannot delete tag with associated items.")
    db.session.delete(tag)
    db.session.commit()
    return {"message": "Tag deleted."}


@mutation.field("linkItemTag")
def resolve_link_item_tag(_, info, itemId, tagId):
    item = ItemModel.query.get(itemId)
    tag = TagModel.query.get(tagId)
    if not item or not tag:
        raise GraphQLError("Invalid item or tag.")
    item.tags.append(tag)
    db.session.add(item)
    db.session.commit()
    return tag


@mutation.field("unlinkItemTag")
def resolve_unlink_item_tag(_, info, itemId, tagId):
    item = ItemModel.query.get(itemId)
    tag = TagModel.query.get(tagId)
    if not item or not tag:
        raise GraphQLError("Invalid item or tag.")
    item.tags.remove(tag)
    db.session.commit()
    return {"message": "Item unlinked from tag."}


# ---------------- User & Auth ----------------
@mutation.field("registerUser")
def resolve_register_user(_, info, username, email, password, role=None):
    if UserModel.query.filter(
        (UserModel.username == username) | (UserModel.email == email)
    ).first():
        raise GraphQLError("User with this username or email already exists.")
    try:
        role_enum = UserRole(role) if role else UserRole.USER
    except ValueError:
        role_enum = UserRole.USER

    user = UserModel(
        username=username,
        email=email,
        password=pbkdf2_sha256.hash(password),
        role=role_enum
    )
    db.session.add(user)
    db.session.commit()
    return {"message": "User created successfully."}


@mutation.field("login")
def resolve_login(_, info, username, password):
    user = UserModel.query.filter(UserModel.username == username).first()
    if not user or not pbkdf2_sha256.verify(password, user.password):
        raise GraphQLError("Invalid credentials.")
    access_token = create_access_token(identity=user.id, fresh=True)
    refresh_token = create_refresh_token(identity=user.id)
    return {"accessToken": access_token, "refreshToken": refresh_token}


@mutation.field("refreshToken")
@jwt_required(refresh=True)
def resolve_refresh_token(_, info):
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    return {"accessToken": new_token, "refreshToken": new_token}
