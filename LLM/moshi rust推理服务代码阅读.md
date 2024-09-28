仓库: https://github.dev/kyutai-labs/moshi

# rust/[moshi-backend](https://github.com/kyutai-labs/moshi/tree/main/rust/moshi-backend)初始化
## Command::Standalone

配置读取后，下载需要的模型
```rust
	// 下载并解压缩 dist.tgz
	if !std::path::PathBuf::from(&config.static_dir).exists() {
		use hf_hub::api::tokio::Api;
		let api = Api::new()?;
		let repo = api.model("kyutai/moshi-artifacts".to_string());
		let dist_tgz = repo.get("dist.tgz").await?;
		if let Some(parent) = dist_tgz.parent() {
			let dist = parent.join("dist");
			if !dist.exists() {
				let output = std::process::Command::new("tar")
					.arg("-xzf")
					.arg(&dist_tgz)
					.arg("-C")
					.arg(parent)
					.output()?;
			}

			config.static_dir = dist.to_string_lossy().to_string()
		}
	}

	standalone::run(&standalone_args, &config).await?;
```

## standalone::run

使用 axum初始化 `/api/chat`，

```rust
    let state = Arc::new(stream_both::AppStateInner::new(args, &config.stream)?);
    tracing::info!("serving static dir {}", config.static_dir);
    let app = axum::Router::new()
        .route("/api/chat", axum::routing::get(stream_handler))
        .layer(tower::ServiceBuilder::new().layer(
	        tower_http::trace::TraceLayer::new_for_http()))
        .with_state(state);

pub async fn stream_handler(
    ws: ws::WebSocketUpgrade,
    axum::extract::ConnectInfo(addr): axum::extract::ConnectInfo<std::net::SocketAddr>,
    state: axum::extract::State<stream_both::AppState>,
    req: axum::extract::Query<stream_both::SessionConfigReq>,
) -> impl axum::response::IntoResponse {
    tracing::info!(?addr, "received connection");
    let sm = stream_both::StreamingModel::new(&state.0, req.0);
    ws.on_upgrade(move |v| handle_socket(v, sm))
}
```

stream_handler 中创建 `stream_both::StreamingModel`，看起来这个model用于管理双向会话，然后通过 `handle_socket(v, sm)` 来处理回包

双向实现核心代码：[moshi/rust/moshi-backend/src/stream_both.rs](https://github.com/kyutai-labs/moshi/blob/main/rust/moshi-backend/src/stream_both.rs)