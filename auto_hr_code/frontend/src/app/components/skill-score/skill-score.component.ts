import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-skill-score',
  templateUrl: './skill-score.component.html',
  styleUrls: ['./skill-score.component.scss']
})
export class SkillScoreComponent {


  @Input() title: any;
  @Input() isBold: any = null;
  @Input() color: any
  @Input() score: any;
  @Input() innerTitle: any;


  ngOnInit(){

    this.isBold = this.isBold === 'false' ? false : true;
  
    this.score = Number(this.score) * 100;
  }

  ngOnChanges(){
    this.isBold = this.isBold === 'false' ? false : true;
  
    this.score = Number(this.score) * 100;
  }


}
