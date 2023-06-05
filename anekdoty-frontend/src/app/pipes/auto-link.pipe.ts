import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'autoLink'
})
export class AutoLinkPipe implements PipeTransform {
  transform(text: string, category: any): string {
    let updatedText = text;
    
    category.sub_categories.forEach((subcategory: any) => {
      subcategory.tags.forEach((tag: any) => {
        if (tag.seo_keywords) {
          const keywords: { [key: string]: string } = {};
          tag.seo_keywords.split(',').forEach((keyword: string) => {
            const urlParams = {
              language_url: category.language.url,
              category_url: category.url,
              subcategory_url: subcategory.url,
              tag_url: tag.url,
              subtag_url: '',
            };
            if (tag.only_subtag) {
              urlParams.subtag_url = keyword.trim(); // Use keyword as the subtag URL
            }
            const url = this.generateUrl(urlParams);
            keywords[keyword.trim()] = url;
          });

          Object.entries(keywords).forEach(([keyword, url]) => {
            const regex = new RegExp(`\\b${keyword}\\b`, 'g');
            updatedText = updatedText.replace(regex, `<a href="${url}">${keyword}</a>`);
          });
        }
      });
    });

    return updatedText;
  }

  private generateUrl(params: any): string {
    const { language_url, category_url, subcategory_url, tag_url, subtag_url } = params;
    let url = `${language_url}/${category_url}`;
    if (subcategory_url) {
      url += `/${subcategory_url}`;
    }
    if (tag_url) {
      url += `/${tag_url}`;
    }
    if (subtag_url) {
      url += `/${subtag_url}`;
    }
    return url;
  }
}
