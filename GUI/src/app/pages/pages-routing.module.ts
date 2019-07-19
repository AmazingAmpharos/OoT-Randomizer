import { RouterModule, Routes } from '@angular/router';
import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

import { PagesComponent } from './pages.component';
import { GeneratorComponent } from './generator/generator.component';

const routes: Routes = [{
  path: '',
  component: PagesComponent,
  children: [
    {
      path: 'generator',
      component: GeneratorComponent,
    },
    {
      path: '',
      redirectTo: 'generator',
      pathMatch: 'full',
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})
export class PagesRoutingModule {
}
