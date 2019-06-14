import { Component } from '@angular/core';
import { GUIGlobal } from '../../../providers/GUIGlobal';

@Component({
  selector: 'ngx-footer',
  styleUrls: ['./footer.component.scss'],
  template: `
    <span>Version <b>{{version}}</b> © ZeldaSpeedRuns Community</span>

    <div class="socials">
      <a href="https://wiki.ootrandomizer.com" target="_blank" class="fab fa-wikipedia-w"></a>
      <a href="https://www.patreon.com/zeldaspeedruns" target="_blank" class="fab fa-patreon"></a>
      <a href="https://discord.gg/xcw9kZm" target="_blank" class="fab fa-discord"></a>
      <a href="https://twitter.com/zeldaspeedruns" target="_blank" class="fab fa-twitter"></a>
      <a href="https://twitch.tv/zeldaspeedruns" target="_blank" class="fab fa-twitch"></a>
      <a href="https://www.youtube.com/channel/UCd3Qyn3yRGaOzEIZojyq2CA" target="_blank" class="ion ion-social-youtube"></a>
    </div>
  `,
})
export class FooterComponent {

  version: string = "";

  constructor(public global: GUIGlobal) { }

  ngOnInit() {

    if (this.global.getGlobalVar('electronAvailable')) {

      this.global.globalEmitter.subscribe(eventObj => {

        if (eventObj.name == "local_version_checked") {
          this.version = eventObj.version;
        }
      });
    }
  }
}
