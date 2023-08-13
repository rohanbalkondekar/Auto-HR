import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewInterviewApplicantsComponent } from './view-interview-applicants.component';

describe('ViewInterviewApplicantsComponent', () => {
  let component: ViewInterviewApplicantsComponent;
  let fixture: ComponentFixture<ViewInterviewApplicantsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ViewInterviewApplicantsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewInterviewApplicantsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
