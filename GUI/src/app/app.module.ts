import { APP_BASE_HREF } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { NbDialogModule } from '@nebular/theme/components/dialog';

import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent, BypassSecurityPipe } from './app.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { ThemeModule } from './@theme/theme.module';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { CdkTableModule } from '@angular/cdk/table';
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

//Pages
import { GUIGlobal } from './providers/GUIGlobal';

//Custom Components
import { ProgressWindow } from './pages/generator/progressWindow/progressWindow.component';
import { DialogWindow } from './pages/generator/dialogWindow/dialogWindow.component';
import { ConfirmationWindow } from './pages/generator/confirmationWindow/confirmationWindow.component';
import { TextInputWindow } from './pages/generator/textInputWindow/textInputWindow.component';

@NgModule({
  declarations: [
    AppComponent,
    BypassSecurityPipe,
    ProgressWindow,
    DialogWindow,
    ConfirmationWindow,
    TextInputWindow
  ],
  entryComponents: [
    ProgressWindow,
    DialogWindow,
    ConfirmationWindow,
    TextInputWindow
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    CdkTableModule,
    NgbModule.forRoot(),
    ThemeModule.forRoot(),
    NbDialogModule.forRoot()
  ],
  exports: [
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
  ],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA
  ],
  providers: [
    { provide: APP_BASE_HREF, useValue: '/' },
    GUIGlobal
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
