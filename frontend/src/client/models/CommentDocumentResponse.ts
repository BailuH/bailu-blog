/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { CommentDocument } from './CommentDocument';
import type { PydanticObjectId } from './PydanticObjectId';
import type { UserDocument } from './UserDocument';

/**
 * fetch_links=True 时的响应模型
 */
export type CommentDocumentResponse = {
    /**
     * MongoDB document ObjectID
     */
    _id?: (PydanticObjectId | null);
    content: string;
    author: UserDocument;
    disabled?: boolean;
    is_reply?: boolean;
    replies: Array<CommentDocument>;
    created_at?: (string | null);
    updated_at?: (string | null);
};

