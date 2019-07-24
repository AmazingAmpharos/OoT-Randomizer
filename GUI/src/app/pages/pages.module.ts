import { NgModule } from '@angular/core';

import { PagesComponent } from './pages.component';
import { GeneratorModule } from './generator/generator.module';
import { PagesRoutingModule } from './pages-routing.module';
import { ThemeModule } from '../@theme/theme.module';

const PAGES_COMPONENTS = [
  PagesComponent
];

@NgModule({
  imports: [
    PagesRoutingModule,
    ThemeModule,
    GeneratorModule
  ],
  declarations: [
    ...PAGES_COMPONENTS,
  ],
})
export class PagesModule {
}
