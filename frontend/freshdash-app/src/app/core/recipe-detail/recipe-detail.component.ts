import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import {NgForOf, NgIf} from '@angular/common';
import {FormsModule} from "@angular/forms";

@Component({
  selector: 'app-recipe-detail',
  templateUrl: './recipe-detail.component.html',
  standalone: true,
  imports: [
    NgIf,
    FormsModule,
    NgForOf
  ],
  styleUrls: ['./recipe-detail.component.css']
})
export class RecipeDetailComponent implements OnInit {
  recipe: any;
  location: string = '';


  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      this.recipe = JSON.parse(params['recipe']);
      this.location = params['location'];
    });
  }
}
