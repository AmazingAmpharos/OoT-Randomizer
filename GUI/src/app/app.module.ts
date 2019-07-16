import { APP_BASE_HREF } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule, ComponentFactoryResolver, ApplicationRef, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
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
import { ErrorDetailsWindow } from './pages/generator/errorDetailsWindow/errorDetailsWindow.component';
import { ConfirmationWindow } from './pages/generator/confirmationWindow/confirmationWindow.component';
import { TextInputWindow } from './pages/generator/textInputWindow/textInputWindow.component';


@NgModule({
  declarations: [
    AppComponent,
    BypassSecurityPipe,
    ProgressWindow,
    DialogWindow,
    ErrorDetailsWindow,
    ConfirmationWindow,
    TextInputWindow
  ],
  entryComponents: [
    AppComponent,
    ProgressWindow,
    DialogWindow,
    ErrorDetailsWindow,
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
  ]
})
export class AppModule {

  constructor(private resolver: ComponentFactoryResolver) { }

  ngDoBootstrap(appRef: ApplicationRef) { //Custom bootstrapper allows to intialize multiple instances of the same app, e.g. generator and patcher
    const factory = this.resolver.resolveComponentFactory(AppComponent);
    const selectorName = factory.selector;

    let elements = document.getElementsByTagName(selectorName);

    //Return if no elements found
    if (elements.length == 0) {
      return;
    }

    //More than one root level component found, bootstrap unique instances
    if (elements.length > 1) {

      for (let i = 0; i < elements.length; i++) {
        console.log("Bootstrap:", elements[i].id);
        appRef.bootstrap(factory, elements[i]);
      }
    }
    else { //Only a single root level component found, bootstrap as usual
      console.log("Bootstrap single GUI app");
      appRef.bootstrap(factory);
    }
  }
}
