# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-07 02:37
from __future__ import unicode_literals

from django.db import migrations

import random




def load_projects(apps, schema_editor):
	Project = apps.get_model("projectapp", "Project")
	User = apps.get_model("authapp", "User")

	tag_list = [i for i in range(1, 51)]

	users = User.objects.all()
	app_project = Project(
		title = "Duis pellentesque neque quis", 
		summary = "Morbi vitae dui purus. Duis nisl ante, varius quis varius sed, fermentum sit amet quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse eget ornare sapien. Maecenas vestibulum lorem vel sem ornare porta. Nunc efficitur sem in quam lobortis iaculis.",
		advantages = "Interdum et malesuada fames ac ante ipsum primis in faucibus. Sed eu ullamcorper dolor, nec commodo elit. Praesent eget sagittis est. Praesent eget cursus purus.",
		investment = "$100 - $300 USD",
		user  = users[0],
		mark = 2.5
	)
	app_project.save()
	for tag in random.sample(tag_list,  random.randint(1, 7)):
		app_project.tags.add(tag)
	app_project = Project(
		title = "Lorem ipsum dolor sit", 
		summary = "Morbi vitae dui purus. Duis nisl ante, varius quis varius sed, fermentum sit amet quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse eget ornare sapien. Maecenas vestibulum lorem vel sem ornare porta. Nunc efficitur sem in quam lobortis iaculis.",
		advantages = "Interdum et malesuada fames ac ante ipsum primis in faucibus. Sed eu ullamcorper dolor, nec commodo elit. Praesent eget sagittis est. Praesent eget cursus purus.",
		investment = "$100 - $300 USD",
		user  = users[0],
		mark = 3.0
	)
	app_project.save()
	for tag in random.sample(tag_list,  random.randint(1, 7)):
		app_project.tags.add(tag)
	app_project = Project(
		title = "Sed non suscipit elit", 
		summary = "Morbi vitae dui purus. Duis nisl ante, varius quis varius sed, fermentum sit amet quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse eget ornare sapien. Maecenas vestibulum lorem vel sem ornare porta. Nunc efficitur sem in quam lobortis iaculis.",
		advantages = "Interdum et malesuada fames ac ante ipsum primis in faucibus. Sed eu ullamcorper dolor, nec commodo elit. Praesent eget sagittis est. Praesent eget cursus purus.",
		investment = "$100 - $300 USD",
		user  = users[0],
		mark = 1.0
	)
	app_project.save()
	for tag in random.sample(tag_list,  random.randint(1, 7)):
		app_project.tags.add(tag)
	app_project = Project(
		title = "Morbi mollis dignissim eros ac", 
		summary = "Morbi vitae dui purus. Duis nisl ante, varius quis varius sed, fermentum sit amet quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse eget ornare sapien. Maecenas vestibulum lorem vel sem ornare porta. Nunc efficitur sem in quam lobortis iaculis.",
		advantages = "Interdum et malesuada fames ac ante ipsum primis in faucibus. Sed eu ullamcorper dolor, nec commodo elit. Praesent eget sagittis est. Praesent eget cursus purus.",
		investment = "$100 - $300 USD",
		user  = users[0],
		mark = 4.5
	)
	app_project.save()
	for tag in random.sample(tag_list,  random.randint(1, 7)):
		app_project.tags.add(tag)
	app_project = Project(
		title = "Orci varius natoque", 
		summary = "Morbi vitae dui purus. Duis nisl ante, varius quis varius sed, fermentum sit amet quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse eget ornare sapien. Maecenas vestibulum lorem vel sem ornare porta. Nunc efficitur sem in quam lobortis iaculis.",
		advantages = "Interdum et malesuada fames ac ante ipsum primis in faucibus. Sed eu ullamcorper dolor, nec commodo elit. Praesent eget sagittis est. Praesent eget cursus purus.",
		investment = "$100 - $300 USD",
		user  = users[0],
		mark = 4.0
	)
	app_project.save()
	for tag in random.sample(tag_list,  random.randint(1, 7)):
		app_project.tags.add(tag)
	app_project = Project(
		title = "parturient montes", 
		summary = "Morbi vitae dui purus. Duis nisl ante, varius quis varius sed, fermentum sit amet quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse eget ornare sapien. Maecenas vestibulum lorem vel sem ornare porta. Nunc efficitur sem in quam lobortis iaculis.",
		advantages = "Interdum et malesuada fames ac ante ipsum primis in faucibus. Sed eu ullamcorper dolor, nec commodo elit. Praesent eget sagittis est. Praesent eget cursus purus.",
		investment = "$100 - $300 USD",
		user  = users[0],
		mark = 1.5
	)
	app_project.save()
	for tag in random.sample(tag_list,  random.randint(1, 7)):
		app_project.tags.add(tag)
	app_project = Project(
		title = "Maecenas vestibulum lorem", 
		summary = "Morbi vitae dui purus. Duis nisl ante, varius quis varius sed, fermentum sit amet quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse eget ornare sapien. Maecenas vestibulum lorem vel sem ornare porta. Nunc efficitur sem in quam lobortis iaculis.",
		advantages = "Interdum et malesuada fames ac ante ipsum primis in faucibus. Sed eu ullamcorper dolor, nec commodo elit. Praesent eget sagittis est. Praesent eget cursus purus.",
		investment = "$100 - $300 USD",
		user  = users[0],
		mark = 2.5
	)
	app_project.save()
	for tag in random.sample(tag_list,  random.randint(1, 7)):
		app_project.tags.add(tag)
	app_project = Project(
		title = "Nullam ligula quam luctus ac", 
		summary = "Morbi vitae dui purus. Duis nisl ante, varius quis varius sed, fermentum sit amet quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse eget ornare sapien. Maecenas vestibulum lorem vel sem ornare porta. Nunc efficitur sem in quam lobortis iaculis.",
		advantages = "Interdum et malesuada fames ac ante ipsum primis in faucibus. Sed eu ullamcorper dolor, nec commodo elit. Praesent eget sagittis est. Praesent eget cursus purus.",
		investment = "$100 - $300 USD",
		user  = users[0],
		mark = 3.5
	)
	app_project.save()
	for tag in random.sample(tag_list,  random.randint(1, 7)):
		app_project.tags.add(tag)
	app_project = Project(
		title = "ac accumsan magna turpis id", 
		summary = "Morbi vitae dui purus. Duis nisl ante, varius quis varius sed, fermentum sit amet quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse eget ornare sapien. Maecenas vestibulum lorem vel sem ornare porta. Nunc efficitur sem in quam lobortis iaculis.",
		advantages = "Interdum et malesuada fames ac ante ipsum primis in faucibus. Sed eu ullamcorper dolor, nec commodo elit. Praesent eget sagittis est. Praesent eget cursus purus.",
		investment = "$100 - $300 USD",
		user  = users[0],
		mark = 2.5
	)
	app_project.save()
	for tag in random.sample(tag_list,  random.randint(1, 7)):
		app_project.tags.add(tag)



class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0008_auto_20170706_2145'),
    ]

    operations = [
    	migrations.RunPython(load_projects),
    ]