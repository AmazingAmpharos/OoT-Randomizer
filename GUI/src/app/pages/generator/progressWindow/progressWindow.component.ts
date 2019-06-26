import { Component, Input, ChangeDetectorRef } from '@angular/core';
import { NbDialogRef } from '@nebular/theme';

@Component({
  template: `
    <nb-card class="progress-window">
      <nb-card-header>
      Generating Seed
      <button nbButton class="headerButton" size="xsmall" status="danger" [disabled]="cancellationInProgress" (click)="cancelGeneration()">X</button>
      </nb-card-header>
      <nb-card-body>
        {{ progressMessage }}
        <p></p>
        <nb-progress-bar [value]="progressPercentage" [status]="progressStatus == 0 ? 'info': progressStatus == 1 ? 'success' : 'danger'" [displayValue]="true"></nb-progress-bar>
        <div *ngIf="progressPercentage == 100" class="footerButtonWrapper">
          <button nbButton [disabled]="cancellationInProgress" size="small" status="primary" (click)="cancelGeneration()">OK</button>
        </div>
      </nb-card-body>
    </nb-card>
  `,
  styleUrls: ['./progressWindow.scss'],
})
export class ProgressWindow {

  @Input() dashboardRef: any;

  progressPercentage: number = 0;
  progressStatus: number = 0;
  progressMessage: string = "Starting.";

  cancellationInProgress: boolean = false;
  closed: boolean = false;

  constructor(protected ref: NbDialogRef<ProgressWindow>, private cd: ChangeDetectorRef) {
  }

  refreshLayout() {

    if (this.closed)
      return;

    this.cd.markForCheck();
    this.cd.detectChanges();
  }

  cancelGeneration() {

    this.cancellationInProgress = true;

    if (this.progressStatus == 0) { //Cancel active generation first before closing progress window
      this.dashboardRef.cancelGeneration().then(() => {
        console.log("Generation was cancelled");
        this.closed = true;
        this.ref.close();
      }).catch((err) => {
        console.log("Couldn't cancel the generation, window stays open. Error:", err);
        this.cancellationInProgress = false;
      });
    }
    else {
      this.closed = true;
      this.ref.close();
    }
  }
}
