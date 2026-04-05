/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { PydanticObjectId } from './PydanticObjectId';

/**
 * 创建评论的请求体
 */
export type CommentCreate = {
    content: string;
    article_id: PydanticObjectId;
};

