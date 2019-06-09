import { Component, OnDestroy } from '@angular/core';
import { takeWhile } from 'rxjs/operators';
import {
  NbThemeService,
} from '@nebular/theme';

@Component({
  selector: 'gui-layout',
  styleUrls: ['./gui.layout.scss'],
  template: `
    <nb-layout>
      <nb-layout-header fixed>
        <div class="dragRegion"></div>
        <ngx-header></ngx-header>
      </nb-layout-header>

      <nb-layout-column class="main-content">
        <ng-content select="router-outlet"></ng-content>
      </nb-layout-column>

      <nb-layout-footer fixed>
        <ngx-footer></ngx-footer>
      </nb-layout-footer>
    </nb-layout>
  `,
})
export class GUILayoutComponent implements OnDestroy {

  private alive = true;
  currentTheme: string;

  constructor(protected themeService: NbThemeService) {

    this.themeService.getJsTheme()
      .pipe(takeWhile(() => this.alive))
      .subscribe(theme => {
        this.currentTheme = theme.name;
    });
  }

  ngOnDestroy() {
    this.alive = false;
  }
}
