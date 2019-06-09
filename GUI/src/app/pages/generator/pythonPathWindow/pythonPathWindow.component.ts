import { Component, Input, ElementRef, ViewChild } from '@angular/core';
import { NbDialogRef } from '@nebular/theme';

import { GUIGlobal } from '../../../providers/GUIGlobal';

@Component({
  template: `
    <nb-card class="pythonPath-window">
      <nb-card-header>
      {{ dialogHeader }}
      </nb-card-header>
      <nb-card-body>
        {{ dialogMessage }}
        <p></p>
        <input #inputBar class="pathInput" type="text" maxlength="260" nbInput fieldSize="small" [(ngModel)]="pythonPath">
        <button class="pathBrowseButton" nbButton status="info" size="small" (click)="browseForPythonFolder()">Browse</button>
      </nb-card-body>
      <nb-card-footer>
        <div class="footerButtonWrapper">
          <button nbButton hero size="small" status="primary" (click)="confirmPath()">OK</button>
        </div>
      </nb-card-footer>
    </nb-card>
  `,
  styleUrls: ['./pythonPathWindow.scss'],
})
export class PythonPathWindow {

  @Input() dialogHeader: string = "Enter python path";
  @Input() dialogMessage: string = "Please enter the path to your local python (>= 3.6) installation:";

  pythonPath: string = "";

  @ViewChild("inputBar") inputBarRef: ElementRef;

  constructor(protected ref: NbDialogRef<PythonPathWindow>, public global: GUIGlobal) {
  }

  ngOnInit() {
    this.inputBarRef.nativeElement.focus();
  }

  browseForPythonFolder() {
    console.log("open folder prompt");

    this.global.browseForDirectory().then(res => {
      this.pythonPath = res;
    }).catch(err => {
      console.log(err);
    });
  }

  confirmPath() {
    //test python path, then close
    console.log(this.pythonPath);
    this.ref.close();
  }
}
