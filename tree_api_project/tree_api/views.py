from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

from .models import Tree
from .serializers import TreeSerializer


@api_view(["GET"])
def get_subtree(request, node_id):
    """
    The `get_subtree` function retrieves a subtree from a specified node in a tree structure.
    :param request: The `request` parameter represents the HTTP request object that contains information
    about the current request, such as headers, body, and user information
    :param node_id: The `node_id` parameter represents the unique identifier of the node that needs to
    be retrieved from the tree structure
    :return: a JsonResponse object with a status code of 200 (OK) if the subtree is successfully retrieved.
    If the node does not exist, a JsonResponse object with a status code of 404 (NOT FOUND) is returned.
    """
    try:
        node = Tree.objects.get(pk=node_id)
    except Tree.DoesNotExist:
        return JsonResponse(
            {"error": "Node not found"}, status=status.HTTP_404_NOT_FOUND
        )

    def get_subtree_helper(node):
        """
        The function `get_subtree_helper` retrieves a subtree from a specified node in a tree structure.

        :param node: The "node" parameter represents a node in a tree structure
        """
        data = TreeSerializer(node).data
        data["children"] = []
        for child in node.children.all():
            data["children"].append(get_subtree_helper(child))
        return data

    subtree = get_subtree_helper(node)

    return JsonResponse(subtree, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_node(request, value):
    try:
        get_node_info = Tree.objects.get(value=value)
        node = {
            "id": get_node_info.id,
            "value": get_node_info.value,
            "deleted": get_node_info.deleted,
            "parent": get_node_info.parent,
        }
        return JsonResponse({"node": node}, status=status.HTTP_200_OK)
    except Tree.DoesNotExist:
        return JsonResponse(
            {"error": "Node not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
def add_node(request):
    """
    The function `add_node` receives a request, validates the data using a serializer, saves the data if
    it is valid, and returns a response with the saved data or any errors encountered.

    :param request: The `request` parameter is an object that represents the HTTP request made to the
    server. It contains information such as the request method (e.g., GET, POST), headers, query
    parameters, and the request body. In this case, it is used to pass the data for creating a new node
    :return: a Response object. If the serializer is valid, it returns the serialized data with a status
    code of 201 (HTTP_CREATED). If the serializer is not valid, it returns the serializer errors with a
    status code of 400 (HTTP_BAD_REQUEST).
    """
    serializer = TreeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_subnode(request, node_parent_id):
    """
    The `create_subnode` function receives a request, validates the data using a serializer, creates a new
    subnode under the node with the given `node_id`, and returns a response with the saved data or any
    errors encountered.

    :param request: The `request` parameter is an object that represents the HTTP request made to the
    server. It contains information such as the request method (e.g., GET, POST), headers, query
    parameters, and the request body. In this case, it is used to pass the data for creating a new subnode
    :param node_id: The `node_id` parameter represents the unique identifier of the node under which the
    new subnode needs to be created
    :return: a Response object. If the serializer is valid, it returns the serialized data with a status
    code of 201 (HTTP_CREATED). If the serializer is not valid, it returns the serializer errors with a
    status code of 400 (HTTP_BAD_REQUEST). If the node with the given `node_id` does not exist, it returns
    a Response object with a status code of 404 (NOT FOUND).
    """
    try:
        parent_node = Tree.objects.get(pk=node_parent_id)
    except Tree.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TreeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(parent=parent_node)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@transaction.atomic
def reset_tree(request):
    """
    The `reset_tree` function resets the tree to its default state, with 4 levels and 10 nodes.
    :param request: The `request` parameter represents the HTTP request object that contains information
    about the current request, such as headers, body, and user information
    :return: a JsonResponse object with a status code of 200 (OK) if the tree is successfully reset.
    """
    # Delete all nodes in the tree
    Tree.objects.all().delete()

    # Create the root node
    root_node = Tree.objects.create(value="root")

    # Create the first level of nodes
    for i in range(1, 10):
        node = Tree.objects.create(value=f"node{i}", parent=root_node)

        # Create the second level of nodes
        for j in range(1, 4):
            child_node = Tree.objects.create(value=f"node{i}.{j}", parent=node)

            # Create the third level of nodes
            for k in range(1, 4):
                grandchild_node = Tree.objects.create(
                    value=f"node{i}.{j}.{k}", parent=child_node
                )

                # Create the fourth level of nodes
                for l in range(1, 4):
                    great_grandchild_node = Tree.objects.create(
                        value=f"node{i}.{j}.{k}.{l}", parent=grandchild_node
                    )

    node = Tree.objects.get(value="node1")

    def get_subtree_helper(node):
        """
        The function `get_subtree_helper` retrieves a subtree from a specified node in a tree structure.

        :param node: The "node" parameter represents a node in a tree structure
        """
        data = TreeSerializer(node).data
        data["children"] = []
        for child in node.children.all():
            data["children"].append(get_subtree_helper(child))
        return data

    subtree = get_subtree_helper(node)
    return JsonResponse(
        {"message": "Tree reset successfully", "reset_node": subtree},
        status=status.HTTP_200_OK,
    )


@api_view(["PUT"])
def change_node_value(request, node_id):
    """
    The `change_node_value` function receives a request, validates the data using a serializer, and updates
    the value of the node with the given `node_id`. It returns a response with the updated data or any
    errors encountered.

    :param request: The `request` parameter represents the HTTP request object that contains information
    about the current request, such as headers, body, and user information
    :param node_id: The `node_id` parameter represents the unique identifier of the node that needs to
    be updated
    :return: a Response object. If the serializer is valid, it returns the serialized data with a status
    code of 200 (HTTP_OK). If the serializer is not valid, it returns the serializer errors with a
    status code of 400 (HTTP_BAD_REQUEST). If the node with the given `node_id` does not exist, it returns
    a Response object with a status code of 404 (NOT FOUND).
    """
    try:
        node = Tree.objects.get(pk=node_id)
    except Tree.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TreeSerializer(node, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def restore_deleted_node(request, node_id):
    """
    The `restore_deleted_node` function receives a request and restores a deleted node and all its subnodes
    that belong to it. It returns a response with the restored data or any errors encountered.

    :param request: The `request` parameter represents the HTTP request object that contains information
    about the current request, such as headers, body, and user information
    :param node_id: The `node_id` parameter represents the unique identifier of the node that needs to
    be restored
    :return: a Response object. If the node with the given `node_id` and all its subnodes are successfully
    restored, it returns a status code of 200 (HTTP_OK). If the node with the given `node_id` does not exist,
    it returns a Response object with a status code of 404 (NOT FOUND).
    """
    try:
        node = Tree.objects.get(pk=node_id)
    except Tree.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    def restore_node(node):
        """
        The function `restore_node` restores a node and all its subnodes that belong to it.

        :param node: The "node" parameter represents a node in a tree structure
        """
        node.deleted = False
        node.save()
        for child in node.children.all():
            restore_node(child)

    restore_node(node)

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_node(request, node_id):
    """
    The `delete_node` function marks a node and all its children as deleted in a tree structure.
    :param request: The `request` parameter represents the HTTP request object that contains information
    about the current request, such as headers, body, and user information
    :param node_id: The `node_id` parameter represents the unique identifier of the node that needs to
    be deleted from the tree structure
    :return: a Response object with a status code of 204 (NO CONTENT) if the node is successfully marked
    as deleted. If the node does not exist, a Response object with a status code of 404 (NOT FOUND) is
    returned.
    """
    try:
        node = Tree.objects.get(pk=node_id)
    except Tree.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    def mark_deleted(node):
        """
        The function `mark_deleted` marks a node as deleted and recursively marks all its children as
        deleted.

        :param node: The "node" parameter represents a node in a tree structure
        """
        node.deleted = True
        node.save()
        for child in node.children.all():
            mark_deleted(child)

    mark_deleted(node)

    return Response(status=status.HTTP_204_NO_CONTENT)
