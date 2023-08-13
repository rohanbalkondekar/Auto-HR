import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HrJobsComponent } from './hr-jobs.component';

describe('HrJobsComponent', () => {
  let component: HrJobsComponent;
  let fixture: ComponentFixture<HrJobsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HrJobsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HrJobsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
