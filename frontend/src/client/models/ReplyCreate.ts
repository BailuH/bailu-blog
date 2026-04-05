/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { PydanticObjectId } from './PydanticObjectId';

/**
 * 创建评论回复的请求体
 */
export type ReplyCreate = {
    content: string;
    parent_comment_id: PydanticObjectId;
};

