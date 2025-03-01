import { inject, Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface Recipe {
  GlutenFree: boolean;
  'High Protein': boolean;
  Ingredients: string;
  Keto: boolean;
  Location: string;
  Recipe: string;
  Spicy: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class RecipeService {

  api: string = environment.apiUrl + '/recipes';
  http: HttpClient = inject(HttpClient);

  getRecipes(location: string): Observable<Recipe[]> {
    return this.http.post<Recipe[]>(this.api, { location });
  }
}
