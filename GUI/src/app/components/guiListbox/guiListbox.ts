import { Component } from '@angular/core';
import { DualListComponent } from 'angular-dual-listbox';

@Component({
  selector: 'gui-listbox',
  templateUrl: './guiListbox.html',
  styleUrls: ['./guiListbox.scss']
})
export class GUIListboxModule extends DualListComponent {
}
