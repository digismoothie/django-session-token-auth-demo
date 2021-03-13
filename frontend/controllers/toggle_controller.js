import { Controller } from 'stimulus';

export default class extends Controller {
  static targets = ['content'];
  static values = { class: String };

  toggle() {
    this.contentTargets.forEach((t) => t.classList.toggle(this.classValue));
  }
}
