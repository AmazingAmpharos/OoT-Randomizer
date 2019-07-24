import { Component } from '@angular/core';
import { MENU_ITEMS } from './pages-menu';

@Component({
  selector: 'ngx-pages',
  template: `
    <gui-layout>
      <router-outlet></router-outlet>
    </gui-layout>
  `,
})
export class PagesComponent {
  menu = MENU_ITEMS;
}
