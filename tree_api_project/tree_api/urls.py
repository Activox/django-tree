from django.urls import path
from .views import (
    get_subtree,
    get_node,
    add_node,
    create_subnode,
    reset_tree,
    change_node_value,
    restore_deleted_node,
    delete_node,
)

urlpatterns = [
    path("get-subtree/<int:node_id>/", get_subtree, name="get-subtree"),
    path("get-node/<str:value>/", get_node, name="get-node"),
    path("add-node/", add_node, name="add-node"),
    path("create-subnode/<int:node_parent_id>/", create_subnode, name="create-subnode"),
    path("reset-tree/", reset_tree, name="reset-tree"),
    path(
        "change-node-value/<int:node_id>/", change_node_value, name="change-node-value"
    ),
    path(
        "restore-deleted-node/<int:node_id>/",
        restore_deleted_node,
        name="restore-deleted-node",
    ),
    path("delete-node/<int:node_id>/", delete_node, name="delete-node"),
]
