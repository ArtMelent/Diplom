import { TestBed } from '@angular/core/testing';

import { CategoryDefaultService } from './category-default.service';

describe('CategoryDefaultService', () => {
  let service: CategoryDefaultService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CategoryDefaultService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
