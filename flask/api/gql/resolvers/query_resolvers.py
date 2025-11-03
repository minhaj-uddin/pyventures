from ariadne import QueryType
from gql.models import StoreModel, ItemModel, TagModel, UserModel

query = QueryType()


# ----- Store -----
@query.field("stores")
def resolve_stores(*_):
    return StoreModel.query.all()


@query.field("store")
def resolve_store(*_, id):
    return StoreModel.query.get(id)


# ----- Item -----
@query.field("items")
def resolve_items(*_):
    return ItemModel.query.all()


@query.field("item")
def resolve_item(*_, id):
    return ItemModel.query.get(id)


# ----- Tag -----
@query.field("tags")
def resolve_tags(*_):
    return TagModel.query.all()


@query.field("tag")
def resolve_tag(*_, id):
    return TagModel.query.get(id)


# ----- User -----
@query.field("users")
def resolve_users(*_):
    return UserModel.query.all()


@query.field("user")
def resolve_user(*_, id):
    return UserModel.query.get(id)
