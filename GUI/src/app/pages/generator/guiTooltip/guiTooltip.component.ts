import { Component, Input } from '@angular/core';

@Component({
  selector: 'gui-tooltip',
  template: `
    <nb-card class="popover-card" style="height:100%;margin-bottom:0px">
      <nb-card-body>
        <span [innerHTML]="tooltip"></span>
      </nb-card-body>
    </nb-card>
  `
})
export class GUITooltip {

  @Input()
  tooltip: string = '';
}
