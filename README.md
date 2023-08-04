# Project Name

django-tree

## Problem description

The purpose of this exercise is to implement endpoints for a REST API that allows performing various operations on a Tree and its nodes. The API development will be carried out using the Django framework to ensure a robust and scalable structure.
Context:
The Tree that will be used in the API consists of a single base node, which cannot be deleted and will have an associated value. Each node of the Tree will be characterized by a field called "value," which will have a maximum length of 30 characters. The Tree can have a maximum of 10 levels of nodes. When deleting a node from the Tree, it should be marked as "deleted," and this condition will also apply to all its child nodes.
Exercise:
The candidate must implement at least three of the following endpoints of the previously described API:
1.  Add a new node to the Tree.
2. Add a new subtree to a specific node of the Tree.
3. Set the value of a particular node in the Tree.
4.  Delete a node from the Tree.
5. Restore a previously deleted node.
6. Restore a previously deleted node and all its child nodes.
7. Restore the Tree to its default state, with 4 levels and 10 nodes.
8. Get a subtree starting from a specified node.
9. Get a subtree starting from a specified node, including all its deleted nodes.

## Installation

To install this project, you will need to have Python and Django installed on your computer. Once you have those installed, you can clone this repository and run the following command:
  1. Clone or Fork the project
  2. cd django-tree
  3. enable the virtual environment on the terminal with `myenv\scripts\active`
  4. then `cd tree_api_project`
  5. then run `python manage.py makemigrations`
  6. `python manage.py migrate`
  7. After this run the test `python manage.py test`
  
  
## Stack used
- python 3.11.0
- django-admin 4.2.4
- djangorestframework 
- django-filter
