import { Component, OnDestroy } from '@angular/core';
import { takeWhile } from 'rxjs/operators';
import {
  NbThemeService,
} from '@nebular/theme';

import { GUIGlobal } from '../../../providers/GUIGlobal';

@Component({
  selector: 'gui-layout',
  styleUrls: ['./gui.layout.scss'],
  template: `
    <nb-layout [ngClass]="{webLayout: !global.getGlobalVar('electronAvailable'), electronLayout: global.getGlobalVar('electronAvailable')}">
      <nb-layout-header fixed *ngIf="global.getGlobalVar('electronAvailable')">
        <div *ngIf="platform != 'darwin' || !isMaximized" class="dragRegion"></div>
        <ngx-header></ngx-header>
      </nb-layout-header>

      <nb-layout-column class="main-content">
        <ng-content select="router-outlet"></ng-content>
      </nb-layout-column>

      <nb-layout-footer fixed *ngIf="global.getGlobalVar('electronAvailable')">
        <ngx-footer></ngx-footer>
      </nb-layout-footer>
    </nb-layout>
  `,
})
export class GUILayoutComponent implements OnDestroy {

  private alive = true;
  currentTheme: string;

  platform: string = (<any>window).apiPlatform;
  isMaximized: boolean = false

  constructor(protected themeService: NbThemeService, public global: GUIGlobal) {

    this.themeService.getJsTheme()
      .pipe(takeWhile(() => this.alive))
      .subscribe(theme => {
        this.currentTheme = theme.name;
    });
  }

  ngOnInit() {

    if (this.global.getGlobalVar('electronAvailable')) {

      this.global.isWindowMaximized().then(res => {
        this.isMaximized = res;
      }).catch((err) => {
        console.log(err);
      });

      this.global.globalEmitter.subscribe(eventObj => {

        if (eventObj.name == "window_maximized") {
          this.isMaximized = true;
        }
        else if (eventObj.name == "window_unmaximized") {
          this.isMaximized = false;
        }
      });
    }
  }

  ngOnDestroy() {
    this.alive = false;
  }
}
