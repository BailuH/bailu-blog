/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ArticleCreateOrUpdate } from '../models/ArticleCreateOrUpdate';
import type { ArticleGenerate } from '../models/ArticleGenerate';
import type { ArticleResponse } from '../models/ArticleResponse';
import type { ArticlesResponse } from '../models/ArticlesResponse';
import type { ArticlesSortField } from '../models/ArticlesSortField';
import type { Body_change_user_role_users__user_id__role_put } from '../models/Body_change_user_role_users__user_id__role_put';
import type { Body_login_for_access_token_token_post } from '../models/Body_login_for_access_token_token_post';
import type { CommentCreate } from '../models/CommentCreate';
import type { CommentResponse } from '../models/CommentResponse';
import type { CommentsResponse } from '../models/CommentsResponse';
import type { CommentsSortField } from '../models/CommentsSortField';
import type { CommentUpdate } from '../models/CommentUpdate';
import type { GeneratedArticleResponse } from '../models/GeneratedArticleResponse';
import type { PydanticObjectId } from '../models/PydanticObjectId';
import type { RegisterRequestBody } from '../models/RegisterRequestBody';
import type { ReplyCreate } from '../models/ReplyCreate';
import type { SortDirection } from '../models/SortDirection';
import type { TokenResponseBody } from '../models/TokenResponseBody';
import type { UpdateUserPasswordRequest } from '../models/UpdateUserPasswordRequest';
import type { UpdateUserRequest } from '../models/UpdateUserRequest';
import type { UserDocument } from '../models/UserDocument';
import type { UserResponse } from '../models/UserResponse';
import type { UsersResponse } from '../models/UsersResponse';
import type { UsersSortField } from '../models/UsersSortField';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class DefaultService {

    /**
     * Login For Access Token
     * 向已认证用户发放访问令牌
     * @param formData
     * @returns TokenResponseBody Successful Response
     * @throws ApiError
     */
    public static loginForAccessTokenTokenPost(
        formData: Body_login_for_access_token_token_post,
    ): CancelablePromise<TokenResponseBody> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Register User
     * 创建新用户
     * @param requestBody
     * @returns UserDocument Successful Response
     * @throws ApiError
     */
    public static registerUserRegisterPost(
        requestBody: RegisterRequestBody,
    ): CancelablePromise<UserDocument> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/register',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * List Articles
     * 返回文章列表。
     * @param skip
     * @param limit
     * @param sortBy
     * @param sortOrder
     * @param tag 用于搜索文章的标签
     * @param searchQuery 用于搜索文章的查询关键词
     * @returns ArticlesResponse Successful Response
     * @throws ApiError
     */
    public static listArticlesArticlesGet(
        skip?: (number | null),
        limit?: (number | null),
        sortBy: ArticlesSortField = 'created_at',
        sortOrder: SortDirection = -1,
        tag?: (string | null),
        searchQuery?: (string | null),
    ): CancelablePromise<ArticlesResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/articles/',
            query: {
                'skip': skip,
                'limit': limit,
                'sort_by': sortBy,
                'sort_order': sortOrder,
                'tag': tag,
                'search_query': searchQuery,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Article
     * 创建新文章。
     * @param requestBody
     * @returns ArticleResponse Successful Response
     * @throws ApiError
     */
    public static createArticleArticlesPost(
        requestBody: ArticleCreateOrUpdate,
    ): CancelablePromise<ArticleResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/articles/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Article
     * 根据 uuid 返回文章。
     * @param articleId
     * @returns ArticleResponse Successful Response
     * @throws ApiError
     */
    public static readArticleArticlesArticleIdGet(
        articleId: PydanticObjectId,
    ): CancelablePromise<ArticleResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/articles/{article_id}',
            path: {
                'article_id': articleId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Article
     * 根据 id 更新文章
     * @param articleId
     * @param requestBody
     * @returns ArticleResponse Successful Response
     * @throws ApiError
     */
    public static updateArticleArticlesArticleIdPut(
        articleId: PydanticObjectId,
        requestBody: ArticleCreateOrUpdate,
    ): CancelablePromise<ArticleResponse> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/articles/{article_id}',
            path: {
                'article_id': articleId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Article
     * 根据 uuid 删除文章
     * @param articleId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteArticleArticlesArticleIdDelete(
        articleId: PydanticObjectId,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/articles/{article_id}',
            path: {
                'article_id': articleId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * List Comments
     * 返回文章评论列表
     * @param articleId
     * @param skip
     * @param limit
     * @param sortBy
     * @param sortOrder
     * @returns CommentsResponse Successful Response
     * @throws ApiError
     */
    public static listCommentsCommentsGet(
        articleId: PydanticObjectId,
        skip?: (number | null),
        limit?: (number | null),
        sortBy: CommentsSortField = 'created_at',
        sortOrder: SortDirection = -1,
    ): CancelablePromise<CommentsResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/comments/',
            query: {
                'article_id': articleId,
                'skip': skip,
                'limit': limit,
                'sort_by': sortBy,
                'sort_order': sortOrder,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Comment
     * 创建文章新评论。
     * @param requestBody
     * @returns CommentResponse Successful Response
     * @throws ApiError
     */
    public static createCommentCommentsPost(
        requestBody: CommentCreate,
    ): CancelablePromise<CommentResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/comments/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Reply
     * 创建评论回复
     * @param requestBody
     * @returns CommentResponse Successful Response
     * @throws ApiError
     */
    public static createReplyCommentsReplyPost(
        requestBody: ReplyCreate,
    ): CancelablePromise<CommentResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/comments/reply',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Comment
     * 根据 id 更新评论
     * @param commentId
     * @param requestBody
     * @returns CommentResponse Successful Response
     * @throws ApiError
     */
    public static updateCommentCommentsCommentIdPut(
        commentId: PydanticObjectId,
        requestBody: CommentUpdate,
    ): CancelablePromise<CommentResponse> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/comments/{comment_id}',
            path: {
                'comment_id': commentId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Comment
     * 根据 id 删除评论
     * @param commentId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteCommentCommentsCommentIdDelete(
        commentId: PydanticObjectId,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/comments/{comment_id}',
            path: {
                'comment_id': commentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * List Users
     * 返回用户列表
     * @param skip
     * @param limit
     * @param sortBy
     * @param sortOrder
     * @returns UsersResponse Successful Response
     * @throws ApiError
     */
    public static listUsersUsersGet(
        skip?: (number | null),
        limit?: (number | null),
        sortBy: UsersSortField = 'created_at',
        sortOrder: SortDirection = -1,
    ): CancelablePromise<UsersResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/',
            query: {
                'skip': skip,
                'limit': limit,
                'sort_by': sortBy,
                'sort_order': sortOrder,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Current User
     * 返回当前用户
     * @returns UserResponse Successful Response
     * @throws ApiError
     */
    public static readCurrentUserUsersMeGet(): CancelablePromise<UserResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/me',
        });
    }

    /**
     * Get User By Id
     * 根据 id 返回用户
     * @param userId 用户 UUID
     * @returns UserResponse Successful Response
     * @throws ApiError
     */
    public static getUserByIdUsersUserIdGet(
        userId: PydanticObjectId,
    ): CancelablePromise<UserResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update User
     * 根据 id 更新用户数据
     * @param userId 用户 UUID
     * @param requestBody
     * @returns UserResponse Successful Response
     * @throws ApiError
     */
    public static updateUserUsersUserIdPut(
        userId: PydanticObjectId,
        requestBody: UpdateUserRequest,
    ): CancelablePromise<UserResponse> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/{user_id}',
            path: {
                'user_id': userId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update User Password
     * 根据 id 更新用户密码
     * @param userId 用户 UUID
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static updateUserPasswordUsersUserIdPasswordPut(
        userId: PydanticObjectId,
        requestBody: UpdateUserPasswordRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/{user_id}/password',
            path: {
                'user_id': userId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Disable User
     * 根据 id 禁用用户 [管理员]
     * @param userId 用户 UUID
     * @returns any Successful Response
     * @throws ApiError
     */
    public static disableUserUsersUserIdDisablePut(
        userId: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/{user_id}/disable',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Change User Role
     * 根据 id 更改用户角色 [管理员]
     * @param userId 用户 UUID
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static changeUserRoleUsersUserIdRolePut(
        userId: string,
        requestBody: Body_change_user_role_users__user_id__role_put,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/{user_id}/role',
            path: {
                'user_id': userId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Generate Article
     * 使用 GPT 模型生成文章
     * @param requestBody
     * @returns GeneratedArticleResponse Successful Response
     * @throws ApiError
     */
    public static generateArticleGptWriterPost(
        requestBody: ArticleGenerate,
    ): CancelablePromise<GeneratedArticleResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/gpt-writer/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
