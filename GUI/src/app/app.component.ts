import { Component, ViewContainerRef, ElementRef, ViewEncapsulation } from '@angular/core';
import { PipeTransform, Pipe } from '@angular/core';
import { Router } from '@angular/router';
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
  template: `<body>
    <router-outlet></router-outlet>
  </body>`,
  styleUrls: ["../app.component.scss"],
  encapsulation: ViewEncapsulation.ShadowDom //Encapsulate in Shadow DOM to prevent style interference on the website
})
export class AppComponent {

  constructor(public viewContainerRef: ViewContainerRef, private elm: ElementRef, private router: Router, private global: GUIGlobal) {
    global.globalInit(elm.nativeElement.id);

    //Route manually at the start to avoid URL changes in the browser
    this.router.navigate(['/pages/generator'], { skipLocationChange: true });
  }
}
