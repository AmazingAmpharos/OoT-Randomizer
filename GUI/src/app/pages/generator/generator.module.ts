import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

import { ThemeModule } from '../../@theme/theme.module';
import { GeneratorComponent } from './generator.component';

import { FlexLayoutModule } from '@angular/flex-layout';

import {
  MatButtonModule,
  MatButtonToggleModule,
  MatCardModule,
  MatCheckboxModule,
  MatDialogModule,
  MatGridListModule,
  MatIconModule,
  MatInputModule,
  MatListModule,
  MatProgressBarModule,
  MatProgressSpinnerModule,
  MatRadioModule,
  MatSelectModule,
  MatSliderModule,
  MatSlideToggleModule,
  MatTableModule
} from '@angular/material';

import { AngularDualListBoxModule } from 'angular-dual-listbox';
import { GUIListboxModule } from '../../components/guiListbox/guiListbox';
import { ColorPickerModule } from 'ngx-color-picker';
import { ngfModule } from "angular-file";

//Custom Directives
import { ResponsiveColsDirective } from '../../directives/responsiveCols.directive';

//Custom Components
import { GUITooltip } from './guiTooltip/guiTooltip.component';

@NgModule({
  imports: [
    ThemeModule,
    MatButtonModule,
    MatButtonToggleModule,
    MatCardModule,
    MatCheckboxModule,
    MatDialogModule,
    MatGridListModule,
    MatIconModule,
    MatInputModule,
    MatListModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatRadioModule,
    MatSelectModule,
    MatSliderModule,
    MatSlideToggleModule,
    MatTableModule,
    FlexLayoutModule,
    ColorPickerModule,
    ngfModule
  ],
  declarations: [
    GeneratorComponent,
    ResponsiveColsDirective,
    GUITooltip,
    GUIListboxModule
  ],
  entryComponents: [
    GUITooltip,
    GUIListboxModule
  ],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ]
})
export class GeneratorModule { }
