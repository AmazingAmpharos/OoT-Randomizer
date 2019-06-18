import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { GUIGlobal } from '../../../providers/GUIGlobal';

@Component({
  selector: 'ngx-header',
  styleUrls: ['./header.component.scss'],
  templateUrl: './header.component.html',
})
export class HeaderComponent {

  isMaximized: boolean = false;
  platform: string = (<any>window).apiPlatform;

  constructor(private cd: ChangeDetectorRef, public global: GUIGlobal) { }

  ngOnInit() {

    if (this.global.getGlobalVar('electronAvailable')) {

      this.global.isWindowMaximized().then(res => {
        this.isMaximized = res;

        this.cd.markForCheck();
        this.cd.detectChanges();
      }).catch((err) => {
        console.log(err);
      });

      this.global.globalEmitter.subscribe(eventObj => {

        if (eventObj.name == "window_maximized") {
          //console.log("maximized event");
          this.isMaximized = true;

          this.cd.markForCheck();
          this.cd.detectChanges();
        }
        else if (eventObj.name == "window_unmaximized") {
          //console.log("unmaximized event");
          this.isMaximized = false;

          this.cd.markForCheck();
          this.cd.detectChanges();
        }
      });
    }
  }

  minimize() {
    this.global.minimizeWindow();
  }

  maximize() {
    this.global.maximizeWindow();
  }

  close() {
    this.global.closeWindow();
  }
}
