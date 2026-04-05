/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { PydanticObjectId } from './PydanticObjectId';

export type CommentDocument = {
    /**
     * MongoDB document ObjectID
     */
    _id?: (PydanticObjectId | null);
    content: string;
    author: ({
        id: string;
        collection: string;
    } | Record<string, any>);
    disabled?: boolean;
    is_reply?: boolean;
    replies?: Array<({
        id: string;
        collection: string;
    } | Record<string, any>)>;
    created_at?: (string | null);
    updated_at?: (string | null);
};

