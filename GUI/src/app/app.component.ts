import { Component, ViewContainerRef } from '@angular/core';
import { PipeTransform, Pipe } from '@angular/core';
import { DomSanitizer } from "@angular/platform-browser";

import { GUIGlobal } from './providers/GUIGlobal';

@Pipe({ name: 'bypassSecurity' })
export class BypassSecurityPipe implements PipeTransform {
  constructor(private sanitizer: DomSanitizer) { }
  transform(url) {
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }
}

@Component({
  selector: 'ngx-app',
  template: '<router-outlet></router-outlet>',
})
export class AppComponent {

  constructor(public viewContainerRef: ViewContainerRef, private global: GUIGlobal) {
  }
}
