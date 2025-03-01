import { Routes } from '@angular/router';
import {HomeComponent} from "./core/home/home.component";
import {LocationDetailComponent} from "./core/location-detail/location-detail.component";

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'location-detail', component: LocationDetailComponent }

];
