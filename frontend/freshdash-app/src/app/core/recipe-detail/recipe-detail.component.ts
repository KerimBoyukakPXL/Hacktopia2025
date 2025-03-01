import {Component, inject, OnInit} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import {NgForOf, NgIf} from '@angular/common';
import {FormsModule} from "@angular/forms";
import {BasketService} from "../../services/basket.service";

@Component({
  selector: 'app-recipe-detail',
  templateUrl: './recipe-detail.component.html',
  standalone: true,
  imports: [
    FormsModule,
    NgForOf,
    NgIf
  ],
  styleUrls: ['./recipe-detail.component.css']
})
export class RecipeDetailComponent implements OnInit {
  recipe: any;
  location: string = '';
  successMessage: string = '';
  basketService: BasketService = inject(BasketService);
  constructor(private route: ActivatedRoute) {}

  getImagePath(recipeName: string): string {
    const formattedName = recipeName.toLowerCase()
      .replace(/\s+/g, '_') // Replace spaces with underscores
      .replace(/[^\w_]/g, ''); // Remove non-alphanumeric characters except underscores
    return `recipes/${formattedName}.webp`;
  }
  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      this.recipe = JSON.parse(params['recipe']);
      this.location = params['location'];
    });
  }
  addToBasket() {
    this.basketService.addToBasket(this.recipe);
  }
}
