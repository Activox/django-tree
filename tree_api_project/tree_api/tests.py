from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import json

from .models import Tree


class TreeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_add_node(self):
        print("\n1. test_add_node")
        url = reverse("add-node")
        data = {"value": "Node 1"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tree.objects.count(), 1)
        self.assertEqual(Tree.objects.get().value, "Node 1")
        node = Tree.objects.get()
        print(
            {
                "id": node.id,
                "value": node.value,
                "deleted": node.deleted,
                "parent": node.parent,
            }
        )

    def test_create_subnode(self):
        print("\n2. test_create_subnode")

        url = reverse("add-node")
        data = {"value": "Node 1"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        tree_node = Tree.objects.get()
        self.assertEqual(tree_node.id, 1)

        parent_node = tree_node

        def create_subnode(parent_node, value):
            url = reverse(
                "create-subnode", kwargs={"node_parent_id": int(parent_node.id)}
            )
            data = {"value": value}
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            return Tree.objects.get(value=value)

        for i in range(2, 11):
            value = f"Node {i}"
            sub_parent_node = create_subnode(parent_node, value)
            for j in range(1, 5):
                value = f"Node {i}.{j}"
                create_subnode(sub_parent_node, value)

        url = reverse("get-subtree", kwargs={"node_id": int(tree_node.id)})
        response = self.client.get(url, format="json")

        self.assertEqual(Tree.objects.count(), 46)

        print(response.json())

    def test_set_node_value(self):
        print("\n3. test_set_node_value")

        node = Tree.objects.create(value="Node 1")
        url = reverse("change-node-value", args=[node.id])
        data = {"value": "New Node Value"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        node.refresh_from_db()
        self.assertEqual(node.value, "New Node Value")
        print(
            {
                "node.value": node.value,
            }
        )

    def test_delete_node(self):
        print("\n4. test_delete_node")

        node = Tree.objects.create(value="Node 1")
        child_node = Tree.objects.create(value="Child Node", parent=node)
        url = reverse("delete-node", args=[node.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        node.refresh_from_db()
        child_node.refresh_from_db()

        self.assertTrue(node.deleted)
        self.assertTrue(child_node.deleted)

    def test_reset_node(self):
        print("\n5. test_reset_node")

        node = Tree.objects.create(value="Node 1")
        child_node = Tree.objects.create(value="Child Node", parent=node)
        url = reverse("reset-tree")
        response = self.client.post(url, format="json")
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        node.refresh_from_db()
        child_node.refresh_from_db()

        self.assertFalse(node.deleted)
        self.assertFalse(child_node.deleted)
