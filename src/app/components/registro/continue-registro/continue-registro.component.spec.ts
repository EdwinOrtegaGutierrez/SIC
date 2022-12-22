import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContinueRegistroComponent } from './continue-registro.component';

describe('ContinueRegistroComponent', () => {
  let component: ContinueRegistroComponent;
  let fixture: ComponentFixture<ContinueRegistroComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ContinueRegistroComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ContinueRegistroComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
