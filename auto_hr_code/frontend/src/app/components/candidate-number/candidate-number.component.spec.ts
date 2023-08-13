import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CandidateNumberComponent } from './candidate-number.component';

describe('CandidateNumberComponent', () => {
  let component: CandidateNumberComponent;
  let fixture: ComponentFixture<CandidateNumberComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CandidateNumberComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CandidateNumberComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
