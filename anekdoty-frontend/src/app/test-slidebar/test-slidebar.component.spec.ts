import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestSlidebarComponent } from './test-slidebar.component';

describe('TestSlidebarComponent', () => {
  let component: TestSlidebarComponent;
  let fixture: ComponentFixture<TestSlidebarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TestSlidebarComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TestSlidebarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
