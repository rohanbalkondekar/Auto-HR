import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SkillScoreComponent } from './skill-score.component';

describe('SkillScoreComponent', () => {
  let component: SkillScoreComponent;
  let fixture: ComponentFixture<SkillScoreComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SkillScoreComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SkillScoreComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
