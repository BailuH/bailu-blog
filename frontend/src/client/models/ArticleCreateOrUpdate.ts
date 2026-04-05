/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * 创建或更新文章的模型。至少必须有一个字段不为 None
 */
export type ArticleCreateOrUpdate = {
    title?: (string | null);
    preview_image_url?: (string | null);
    content?: (string | null);
    tags?: (Array<string> | null);
};

