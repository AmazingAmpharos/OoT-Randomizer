import { Component, Input } from '@angular/core';
import { DualListComponent } from 'angular-dual-listbox';

/*
import {
  Component, DoCheck, EventEmitter, Input, IterableDiffers, OnChanges,
  Output, SimpleChange
} from '@angular/core';
*/

@Component({
  selector: 'gui-listbox',
  templateUrl: './guiListbox.html',
  styleUrls: ['./guiListbox.scss']
})
export class GUIListboxModule extends DualListComponent {

  @Input() tooltip: any = 'tooltip';
  @Input() tooltipComponent: any = null;

  buildAvailable(source: Array<any>): boolean
  {
    const sourceChanges = this.sourceDiffer.diff(source);
    if (sourceChanges) {
      sourceChanges.forEachRemovedItem((r: any) => {
        const idx = this.findItemIndex(this.available.list, r.item, this.key);
        if (idx !== -1) {
          this.available.list.splice(idx, 1);
        }
      });

      sourceChanges.forEachAddedItem((r: any) => {
        // Do not add duplicates even if source has duplicates.
        if (this.findItemIndex(this.available.list, r.item, this.key) === -1) {
          this.available.list.push({ _id: this.makeIdExtended(r.item), _name: this.makeName(r.item), _tooltip: this.makeTooltipExtended(r.item) });
        }
      });

      if (this.compare !== undefined) {
        this.available.list.sort(this.compare);
      }
      this.available.sift = this.available.list;

      return true;
    }
    return false;
  }

  private makeIdExtended(item: any): string | number {
    if (typeof item === 'object') {
      return item[this.key];
    }
    else {
      return item;
    }
  }

  private makeTooltipExtended(item: any): string {
    if (typeof item === 'object') {
      return item[this.tooltip] ? item[this.tooltip] : "";
    }
    else {
      return item;
    }
  }
}
