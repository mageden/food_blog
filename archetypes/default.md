---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
date: {{ .Date }}
draft: true
description: ""
thumbnail: ""
tags: []
# Optional opening paragraphs (shown above the recipe card):
# intro: |
#   Your lead text in **Markdown**.
# Structured recipe (Shape A: ingredient_groups + step_groups, optional prep_time, cook_time, total_time, yield, author, category, cuisine):
# recipe:
#   prep_time: "20 minutes"
#   cook_time: "30 minutes"
#   yield: "4 servings"
#   ingredient_groups:
#     - name: "Component A"
#       items:
#         - "First ingredient"
#     - items:
#         - "Ungrouped ingredients use a list item with only `items`."
#   step_groups:
#     - name: "Mix"
#       steps:
#         - "First step with **Markdown** allowed."
---

Write tips, photos, and notes below the recipe card.
