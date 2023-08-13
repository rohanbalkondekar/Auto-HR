import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResumeJobDetailsComponent } from './resume-job-details.component';

describe('ResumeJobDetailsComponent', () => {
  let component: ResumeJobDetailsComponent;
  let fixture: ComponentFixture<ResumeJobDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ResumeJobDetailsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ResumeJobDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
