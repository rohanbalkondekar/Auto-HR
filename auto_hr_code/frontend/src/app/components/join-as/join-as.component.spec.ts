import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JoinAsComponent } from './join-as.component';

describe('JoinAsComponent', () => {
  let component: JoinAsComponent;
  let fixture: ComponentFixture<JoinAsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ JoinAsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(JoinAsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
