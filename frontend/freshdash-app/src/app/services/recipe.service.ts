import {inject, Injectable} from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class RecipeService {

  api:string = environment.apiUrl + '/recipes';
  http:HttpClient = inject(HttpClient);

  getRecipes(location: string): Observable<any> {
    return this.http.post<any>(this.api, { location });
  }
}
