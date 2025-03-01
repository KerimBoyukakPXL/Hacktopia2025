import { Component, inject, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NgForOf } from '@angular/common';
import {RecipeService} from "../../services/recipe.service";
import {FormsModule} from "@angular/forms";

@Component({
    selector: 'app-location-detail',
    templateUrl: './location-detail.component.html',
    imports: [
        NgForOf,
        FormsModule
    ],
    styleUrls: ['./location-detail.component.css']
})
export class LocationDetailComponent implements OnInit {
  recipeService: RecipeService = inject(RecipeService);
  location: string = '';
  recipes: any[] = [];

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      this.location = params['location'];
      this.getRecipes();
    });
  }

  getRecipes() {
    this.recipeService.getRecipes(this.location).subscribe((data: any) => {
      this.recipes = data;
    });
  }
}
