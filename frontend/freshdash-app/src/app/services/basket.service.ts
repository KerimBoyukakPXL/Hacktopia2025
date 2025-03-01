import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class BasketService {
  private basket: any[] = [];

  addToBasket(item: any) {
    this.basket.push(item);
  }

  getBasket() {
    return this.basket;
  }

  clearBasket() {
    this.basket = [];
  }

  constructor() { }
}
