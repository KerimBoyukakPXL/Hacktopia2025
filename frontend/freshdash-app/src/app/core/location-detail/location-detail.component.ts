import { Component, inject, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RecipeService } from '../../services/recipe.service';
import {NgForOf, NgIf} from '@angular/common';
import {FormsModule} from "@angular/forms";

@Component({
  selector: 'app-location-detail',
  templateUrl: './location-detail.component.html',
  standalone: true,
  imports: [
    NgForOf,
    FormsModule
  ],
  styleUrls: ['./location-detail.component.css']
})
export class LocationDetailComponent implements OnInit {
  recipeService: RecipeService = inject(RecipeService);
  router: Router = inject(Router);
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

  navigateToRecipe(recipe: any) {
    this.router.navigate(['/recipe-detail'], { queryParams: { recipe: JSON.stringify(recipe), location: this.location } });
  }
}
