from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Tree


class TreeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_add_node(self):
        print("\r\nCreate a node")
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
        print("\r\nCreate a node with subnodes")

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

    def test_set_node_new_value(self):
        print("\r\nChange a node Value")

        node = Tree.objects.create(value="Node 1")
        print({"node.value": node.value})
        url = reverse("change-node-value", kwargs={"node_id": int(node.id)})
        data = {"value": "New Node Value"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        node.refresh_from_db()
        self.assertEqual(node.value, "New Node Value")
        print(
            {
                "new node.value": node.value,
            }
        )

    def test_delete_node(self):
        print("\r\nDelete a node")

        node = Tree.objects.create(value="Node 1")
        child_node = Tree.objects.create(value="Child Node", parent=node)
        url = reverse("delete-node", kwargs={"node_id": int(node.id)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        node.refresh_from_db()
        child_node.refresh_from_db()

        self.assertTrue(node.deleted)
        self.assertTrue(child_node.deleted)

    def test_reset_node(self):
        print("\r\nReset a node with 4 levels and 10 nodes")

        node = Tree.objects.create(value="Node 1")
        child_node = Tree.objects.create(value="Child Node", parent=node)
        url = reverse("reset-tree")
        response = self.client.post(url, format="json")
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restore_deleted_node(self):
        print("\r\nRestore a deleted Node")

        node = Tree.objects.create(value="Node 1")
        child_node = Tree.objects.create(value="Child Node", parent=node)
        url = reverse("delete-node", kwargs={"node_id": int(node.id)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        node.refresh_from_db()
        child_node.refresh_from_db()

        self.assertTrue(node.deleted)
        self.assertTrue(child_node.deleted)

        url = reverse("restore-deleted-node", kwargs={"node_id": int(node.id)})
        response = self.client.put(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        node.refresh_from_db()
        child_node.refresh_from_db()

        self.assertFalse(node.deleted)
        self.assertFalse(child_node.deleted)

    def test_obtain_subnode_from_specified_node(self):
        print("\r\nObtain a subnode from specified node")

        node = Tree.objects.create(value="Node 1")
        child_node = Tree.objects.create(value="Child Node", parent=node)
        url = reverse("get-subtree", kwargs={"node_id": int(child_node.id)})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print({"response": response.json()})
        data = response.json()
        self.assertEqual(data["id"], child_node.id)
        self.assertEqual(data["value"], child_node.value)
        self.assertEqual(data["parent"], node.id)

    def test_obtain_subtree_from_specified_node_with_deleted_child(self):
        print("\r\nObtain a subtree from specified node with deleted child")

        node = Tree.objects.create(value="Node 1")
        child_node = Tree.objects.create(value="Child Node", parent=node)
        url = reverse("delete-node", kwargs={"node_id": int(child_node.id)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse("get-subtree", kwargs={"node_id": int(node.id)})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print({"response": response.json()})

        data = response.json()
        self.assertEqual(data["id"], node.id)
        self.assertEqual(data["value"], node.value)
        self.assertEqual(data["parent"], None)
        self.assertEqual(len(data["children"]), 1)
