function [mappedX, mapping] = lle(X, no_dims, k, eig_impl, benchmark)
%LLE Runs the locally linear embedding algorithm
%
%   mappedX = lle(X, no_dims, k, eig_impl)
%
% Runs the local linear embedding algorithm on dataset X to reduces its
% dimensionality to no_dims. In the LLE algorithm, the number of neighbors
% can be specified by k. 
% The function returns the embedded coordinates in mappedX.
%
%

% This file is part of the Matlab Toolbox for Dimensionality Reduction.
% The toolbox can be obtained from http://homepage.tudelft.nl/19j49
% You are free to use, change, or redistribute this code in any way you
% want for non-commercial purposes. However, it is appreciated if you 
% maintain the name of the original author.
%
% (C) Laurens van der Maaten, Delft University of Technology


    if ~exist('no_dims', 'var')
        no_dims = 2;
    end
    if ~exist('k', 'var')
        k = 12;
    end
    if ~exist('eig_impl', 'var')
        eig_impl = 'Matlab';
    end
    if ~exist('benchmark', 'var')
        benchmark = 0;
    end

    % Get dimensionality and number of dimensions
    [n, d] = size(X);

    % Compute pairwise distances and find nearest neighbors (vectorized implementation)
    if ~benchmark
        disp('Finding nearest neighbors...');
    else
        tstart = tic;
    end
    [distance, neighborhood] = find_nn(X, k);
    if benchmark
        fprintf('[benchmark] Neighbors search took %.2f seconds.\n', toc(tstart));
    end

    % Identify largest connected component of the neighborhood graph
    blocks = components(distance)';
    count = zeros(1, max(blocks));
    for i=1:max(blocks)
        count(i) = length(find(blocks == i));
    end
    [count, block_no] = max(count);
    conn_comp = find(blocks == block_no); 

    % Update the neighborhood relations
    tmp = 1:n;
    tmp = tmp(conn_comp);
    new_ind = zeros(n, 1);
    for i=1:n
        ii = find(tmp == i);
        if ~isempty(ii), new_ind(i) = ii; end
    end 
    neighborhood = neighborhood(conn_comp,:)';
    for i=1:n
        neighborhood(neighborhood == i) = new_ind(i);
    end
    n = numel(conn_comp);
    X = X(conn_comp,:)';    
    max_k = size(neighborhood, 1);

    % Find reconstruction weights for all points by solving the MSE problem 
    % of reconstructing a point from each neighbours. A used constraint is 
    % that the sum of the reconstruction weights for a point should be 1.
    if ~benchmark
        disp('Compute reconstruction weights...');
    else
        tweights = tic;
    end
    if k > d 
        tol = 1e-5;
    else
        tol = 0;
    end

    % Construct reconstruction weight matrix
    W = zeros(max_k, n);
    for i=1:n
        nbhd = neighborhood(:,i);
        nbhd = nbhd(nbhd ~= 0);
        kt = numel(nbhd);
        z = bsxfun(@minus, X(:,nbhd), X(:,i));                  % Shift point to origin
        C = z' * z;												% Compute local covariance
        C = C + eye(kt, kt) * tol * trace(C);					% Regularization of covariance (if K > D)
        wi = C \ ones(kt, 1);                                   % Solve linear system
        wi = wi / sum(wi);                                      % Make sure that sum is 1
        W(:,i) = [wi; nan(max_k - kt, 1)];
    end
    if benchmark
        fprintf('[benchmark] LLE weight computation took %.2f seconds.\n', toc(tweights));
    end

    % Now that we have the reconstruction weights matrix, we define the 
    % sparse cost matrix M = (I-W)'*(I-W).
    M = sparse(1:n, 1:n, ones(1, n), n, n, 4 * max_k * n);
    for i=1:n
       w = W(:,i);
       j = neighborhood(:,i);
       indices = find(j ~= 0 & ~isnan(w));
       j = j(indices);
       w = w(indices);
       M(i, j) = M(i, j) - w';
       M(j, i) = M(j, i) - w;
       M(j, j) = M(j, j) + w * w';
    end
	
	% For sparse datasets, we might end up with NaNs or Infs in M. We just set them to zero for now...
	M(isnan(M)) = 0;
	M(isinf(M)) = 0;
    
    % The embedding is computed from the bottom eigenvectors of this cost matrix
    if ~benchmark
        disp('Compute embedding (solve eigenproblem)...');
    else
        teigen = tic;
    end;
    tol = 0;
    if strcmp(eig_impl, 'JDQR')
        options.Disp = 0;
        options.LSolver = 'bicgstab';
        [mappedX, eigenvals] = jdqr(M + eps * eye(n), no_dims + 1, tol, options);
    else
        options.disp = 0;
        options.isreal = 1;
        options.issym = 1;
        [mappedX, eigenvals] = eigs(M + eps * eye(n), no_dims + 1, tol, options);          % only need bottom (no_dims + 1) eigenvectors
    end
    [eigenvals, ind] = sort(diag(eigenvals), 'ascend');
    if benchmark
        fprintf('[benchmark] %s eigendecomposition took %.2f seconds.\n', eig_impl, toc(teigen));
    end
    if size(mappedX, 2) < no_dims + 1
		no_dims = size(mappedX, 2) - 1;
		warning(['Target dimensionality reduced to ' num2str(no_dims) '...']);
    end
    eigenvals = eigenvals(2:no_dims + 1);
    mappedX = mappedX(:,ind(2:no_dims + 1));                                % throw away zero eigenvector/value
    
    % Save information on the mapping
    mapping.k = k;
    mapping.X = X';
    mapping.vec = mappedX;
    mapping.val = eigenvals;
    mapping.conn_comp = conn_comp;
    mapping.nbhd = distance;

    if benchmark
        fprintf('[benchmark] Embedding with LLE took %.2f seconds.\n', toc(tstart));
    end
